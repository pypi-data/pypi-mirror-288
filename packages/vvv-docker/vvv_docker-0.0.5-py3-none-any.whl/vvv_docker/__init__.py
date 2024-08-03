import re
import os
import sys
import json
import time
import random
import threading
import tempfile
lock = threading.RLock()

import paramiko
ssh = None
workspace = '/root/vvv/workspace'
def make_global_ssh(sconfig=None):
    if not sconfig: return False
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    hostname = sconfig.get('hostname', None)
    if not hostname: return False
    username = sconfig.get('username', None)
    if not username: return False
    password = sconfig.get('password', None)
    if not password: return False
    port = int(sconfig.get('port', 22))
    ssh.connect(hostname=hostname, port=port, username=username, password=password)
    return True

def run_cmd(cmd, tg_stdout=True, tp_stderr=True, get_pty=True):
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=get_pty)
    print('------------ run cmd:', cmd)
    start_time = time.time()
    r = []
    if tg_stdout:
        for i in stdout:
            print(i.rstrip())
            r.append(i.rstrip())
    if tp_stderr:
        for i in stderr:
            print(i.rstrip())
    r = '\n'.join(r).strip()
    print('------------ run end costtime:', f'{(time.time() - start_time)*1000:.2f}ms')
    return r

def run_cmd_loop(cmd, fmt=lambda i:i):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    togglea = True
    toggleb = True
    def sout():
        for i in stdout:
            with lock:
                print(fmt(i.rstrip()))
        togglea = False
    def serr():
        for i in stderr:
            with lock:
                print(fmt(i.rstrip()))
        toggleb = False
    a = threading.Thread(target=sout)
    b = threading.Thread(target=serr)
    a.start()
    b.start()
    while togglea and toggleb:
        time.sleep(0.1)

def download_from_server(filepath, serverpath, redownload=False):
    if not redownload and os.path.isfile(filepath):
        print('file exist:', filepath)
        return
    print('------------ run downloadfile:', filepath, serverpath)
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    remote_file_info = sftp.stat(serverpath)
    remote_file_size = remote_file_info.st_size
    start_time = time.time()
    def file_transfer_callback(transferred, total):
        elapsed_time = time.time() - start_time
        speed = transferred / elapsed_time if elapsed_time > 0 else 0
        speed_mbps = speed / (1024 * 1024)  # Convert to MB/s
        print(f"Downloaded {transferred} of {total} bytes ({transferred / total:.2%}), Speed: {speed_mbps:.2f} MB/s")
    sftp.get(serverpath, filepath, callback=file_transfer_callback)

def save_in_server(filepath, serverpath):
    if not os.path.isfile(filepath):
        print('local file not exist:', filepath)
        return
    print('------------ Running save file:', filepath, serverpath)
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    total_size = os.path.getsize(filepath)
    transferred = 0
    buffer_size = 1024 * 1024 # 1M
    start_time = time.time()
    def upload_progress(transferred, total, speed):
        percentage = transferred / total * 100
        print(f"Uploaded {transferred} of {total} bytes ({percentage:.2f}%) at {speed:.2f} KB/s")
    with sftp.open(serverpath, 'wb') as remote_file:
        with open(filepath, 'rb') as local_file:
            while True:
                data = local_file.read(buffer_size)
                if not data:
                    break
                remote_file.write(data)
                transferred += len(data)
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    speed = transferred / 1024 / elapsed_time  # Speed in KB/s
                else:
                    speed = 0
                upload_progress(transferred, total_size, speed)
    sftp.close()

def make_workspace_run_cmd(wksp, sconfig=None):
    make_global_ssh(sconfig)
    run_cmd('mkdir -p ' + wksp)
    def f(a): return run_cmd('cd ' + wksp + ' && ' + a)
    def ro(a): return run_cmd_loop('cd ' + wksp + ' && ' + a)
    def e(a): return run_cmd('cd ' + wksp + ' && ' + '[ -e ' + a + ' ] && echo "exist" || echo "not exist"') == 'exist'
    def l(): return run_cmd('cd ' + wksp + ' && ' + 'ls -lhS')
    def d(a,b,redownload=False): return download_from_server(a, wksp.rstrip('/') + '/' + b, redownload=redownload)
    def u(a,b,reupdate=False): return save_in_server(a, wksp.rstrip('/') + '/' + b)
    def r(a): return run_cmd('cd ' + wksp + ' && ' + 'rm ' + a)
    return f, ro, e, l, d, u, r

def init_worker(wksp=None, sconfig=None):
    if not sconfig:
        if not load_config():
            return
    wksp = wksp or workspace
    wrun_cmd, wrun_cmd_loop, wexist, wls, wdownload, wupdate, wremove = make_workspace_run_cmd(wksp, sconfig=sconfig)
    class _: pass
    _.wrun_cmd = wrun_cmd
    _.wrun_cmd_loop = wrun_cmd_loop
    _.wexist = wexist
    _.wls = wls
    _.wdownload = wdownload
    _.wupdate = wupdate
    _.wremove = wremove
    def write_in_server(code, filename):
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8') as f:
            tfilename = f.name
            f.write(code)
        _.wupdate(tfilename, filename)
        os.remove(tfilename)
    _.wupdate_str = write_in_server
    def wstop_docker(name):
        _.wrun_cmd(f'docker kill {name}')
        _.wrun_cmd(f'docker rm {name}')
    def wupdate_by_type(filepath_or_code, filename, type):
        if type == 'auto':
            import os
            if os.path.isfile(filepath_or_code):
                _.wupdate(filepath_or_code, filename)
            else:
                _.wupdate_str(filepath_or_code, filename)
        elif type == 'file':
            _.wupdate(filepath_or_code, filename)
        elif type == 'str':
            _.wupdate_str(filepath_or_code, filename)
        else:
            raise Exception('not valid type:' + type)
    def wrun_openresty(name, filepath_or_code, ports, type='auto', filename='./nginx.conf', extra=''):
        '''
        ports: ["80:80", "443:443"]
        '''
        ports = ' '.join(['-p' + i for i in ports])
        wupdate_by_type(filepath_or_code, filename, type)
        wstop_docker(name)
        _.wrun_cmd(f'docker run --name {name} {ports} -v {filename}:/usr/local/openresty/nginx/conf/nginx.conf {extra} openresty/openresty:latest')
        _.wrun_cmd_loop(f'docker logs -f {name}')
    def wrun_openresty_ja3(name, filepath_or_code, ports, type='auto', filename='./nginx.conf', extra=''):
        '''
        ports: ["80:80", "443:443"]
        '''
        ports = ' '.join(['-p' + i for i in ports])
        wupdate_by_type(filepath_or_code, filename, type)
        wstop_docker(name)
        _.wrun_cmd(f'docker run --name {name} {ports} -v {filename}:/usr/local/openresty/nginx/conf/nginx.conf {extra} cilame/openresty_ja3:latest')
        _.wrun_cmd_loop(f'docker logs -f {name}')
    def wrun_nodejs(name, filepath_or_code, ports=[], type='auto', filename='./_nodejs.js', extra=''):
        '''
        ports: ["80:80", "443:443"]
        '''
        ports = ' '.join(['-p' + i for i in ports])
        wupdate_by_type(filepath_or_code, filename, type)
        wstop_docker(name)
        _.wrun_cmd(f'docker run --name {name} {ports} -v {filename}:/1.js {extra} node:alpine node /1.js')
        _.wrun_cmd_loop(f'docker logs -f {name}')
    def wrun_python(name, filepath_or_code, ports=[], type='auto', filename='./_python.js', extra=''):
        '''
        ports: ["80:80", "443:443"]
        '''
        ports = ' '.join(['-p' + i for i in ports])
        wupdate_by_type(filepath_or_code, filename, type)
        wstop_docker(name)
        _.wrun_cmd(f'docker run --name {name} {ports} -v {filename}:/1.py {extra} cilame/py310:alpine python /1.py')
        _.wrun_cmd_loop(f'docker logs -f {name}')
    _.wstop_docker = wstop_docker
    _.wupdate_by_type = wupdate_by_type
    _.wrun_openresty = wrun_openresty
    _.wrun_openresty_ja3 = wrun_openresty_ja3
    _.wrun_nodejs = wrun_nodejs
    _.wrun_python = wrun_python
    return _

def test_build():
    r"""
    # 这里用于后续测试使用
    import vvv_docker
    vvv = vvv_docker.init_worker('/root/vvv/buildspace')
    vvv.wrun_cmd('docker pull hub.atomgit.com/amd64/python:3.10-alpine3.17')
    vvv.wupdate_str('''
    FROM hub.atomgit.com/amd64/python:3.10-alpine3.17
    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1
    RUN pip install requests flask -i https://pypi.tuna.tsinghua.edu.cn/simple
    WORKDIR /app
    CMD ["python", "-V"]
    ''', 'Dockerfile')
    vvv.wls()
    vvv.wrun_cmd('docker kill $(docker ps -a -q --filter ancestor=cilame/py310:alpine)')
    vvv.wrun_cmd('docker rm $(docker ps -a -q --filter ancestor=cilame/py310:alpine)')
    vvv.wrun_cmd('docker rmi cilame/py310:alpine')
    vvv.wrun_cmd('docker build -t cilame/py310:alpine .')
    vvv.wrun_cmd('docker images')
    """

def test_python():
    return r"""
import vvv_docker
vvv = vvv_docker.init_worker()
vvv.wrun_python('vvv_test', '''
import requests
s = requests.get('http://baidu.com')
print(s)
''')
    """

def test_nodejs():
    return r"""
import vvv_docker
vvv = vvv_docker.init_worker()
vvv.wrun_nodejs('vvv_test', '''
console.log(123)
''')
    """

def test_nginx(base='openresty'):
    return r"""
import vvv_docker
ngx_cfg = '''
# worker_processes 1;
pcre_jit on;
events {
    worker_connections  1024;
}
http {
    lua_shared_dict __shared__ 10M;
    init_worker_by_lua_block {
        ngx.log(ngx.ERR, 'start')
    }
    server {
        listen 80;
        server_name ~^.*$;
        location / {
            access_by_lua_block { }
            header_filter_by_lua_block { ngx.header['Server'] = nil; ngx.header.content_length = nil }
            content_by_lua_block {
                ngx.header.content_type = 'text/html; charset=utf8'
                ngx.say('start')
                ngx.exit(200)
            }
        }
    }
    server {
        listen 443 ssl;
        server_name ~^.*$;
        ssl_protocols               TLSv1.2 TLSv1.3;
        ssl_ciphers                 HIGH:!aNULL:!MD5;
        ssl_session_cache           shared:SSL:1m;
        ssl_session_timeout         5m;
        ssl_certificate             "data:-----BEGIN CERTIFICATE-----\nMIIBtjCCAV2gAwIBAgIUN/O0uv7B+18ohuf05ygsoC82liswCgYIKoZIzj0EAwIw\nMTELMAkGA1UEBhMCVVMxDDAKBgNVBAsMA1dlYjEUMBIGA1UEAwwLZXhhbXBsZS5v\ncmcwHhcNMjIwNzI4MTgzMzA2WhcNMjMwNzI5MTgzMzA2WjAxMQswCQYDVQQGEwJV\nUzEMMAoGA1UECwwDV2ViMRQwEgYDVQQDDAtleGFtcGxlLm9yZzBZMBMGByqGSM49\nAgEGCCqGSM49AwEHA0IABNCXpLc6YN7Scd4j1NOVsBuBsHgsBlr/O5JGUBgfurxv\n5EEHjoZ2e+0wq6EIGOGVZwUWUw9Jb8Uskeq8Ld5VkOCjUzBRMB0GA1UdDgQWBBSH\n9cc3JRcpyPh3nEa41Ux6RDGjLTAfBgNVHSMEGDAWgBSH9cc3JRcpyPh3nEa41Ux6\nRDGjLTAPBgNVHRMBAf8EBTADAQH/MAoGCCqGSM49BAMCA0cAMEQCIChRR5U7MMYQ\ntMK0zhNnt2SqRy30VcPIm9qoEms5cNxdAiBb273P7vSkj/PmDd1WsFVkg9NymBaT\n0nsIem2LKav60g==\n-----END CERTIFICATE-----\n";
        ssl_certificate_key         "data:-----BEGIN EC PARAMETERS-----\nBggqhkjOPQMBBw==\n-----END EC PARAMETERS-----\n-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIL02pwZutbzkmdIM0QpvD7W3pcL2dGaeWrbQ8pNCHPFeoAoGCCqGSM49\nAwEHoUQDQgAE0Jektzpg3tJx3iPU05WwG4GweCwGWv87kkZQGB+6vG/kQQeOhnZ7\n7TCroQgY4ZVnBRZTD0lvxSyR6rwt3lWQ4A==\n-----END EC PRIVATE KEY-----\n";
        ssl_prefer_server_ciphers   on;
        location / {
            access_by_lua_block { }
            header_filter_by_lua_block { ngx.header['Server'] = nil; ngx.header.content_length = nil }
            content_by_lua_block {
                local function ja3_sort3(data)
                    local tg = ""
                    local gs = {}
                    for g in data:gmatch("[^,]+") do table.insert(gs, g) end
                    if #gs >= 3 then tg = gs[3] else return data end
                    local sn = {}
                    for n in tg:gmatch("%d+") do table.insert(sn, tonumber(n)) end
                    table.sort(sn)
                    gs[3] = table.concat(sn, "-")
                    return table.concat(gs, ",")
                end
                ngx.header.content_type = 'text/html; charset=utf8'
                ngx.say(ja3_sort3(ngx.var.http_ssl_ja3 or "no ja3"))
                ngx.exit(200)
            }
        }
    }
    include             mime.types;
    default_type        application/octet-stream;
    sendfile            on;
    tcp_nopush          off;
    tcp_nodelay         on;
    keepalive_timeout   65;
    server_tokens       off;
    #gzip  on;
    include             /etc/nginx/conf.d/*.conf;
}
'''
vvv = vvv_docker.init_worker()
vvv.wrun_"""+base+"""('vvv_test', ngx_cfg, ["8080:80", "8443:443"])
    """

def make_zipper(wksp):
    def zip2gz(a,b): return run_cmd('cd ' + wksp + ' && ' + 'tar -cvzf ' + b + ' ' + a)
    def zip2xz(a,b): return run_cmd('cd ' + wksp + ' && ' + 'tar -cJf ' + b + ' ' + a)
    def unzipgz(a): return run_cmd('cd ' + wksp + ' && ' + 'tar -xvf ' + a + ' --checkpoint=.1000 --checkpoint-action=echo')
    def unzipxz(a): return run_cmd('cd ' + wksp + ' && ' + 'tar -xJf ' + a + ' --checkpoint=.1000 --checkpoint-action=echo')
    return zip2gz, zip2xz, unzipgz, unzipxz

def download_a_docker(wksp, dockername, localfilename, dockerfilename, ziptype=None):
    # 将 docker 镜像下载到本地
    wrun_cmd, wrun_cmd_loop, wexist, wls, wdownload, wupdate, wremove = make_workspace_run_cmd(wksp)
    wzip2gz, wzip2xz, unzipgz, unzipxz = make_zipper(wksp)
    wrun_cmd('docker images')
    if not wexist(dockerfilename): wrun_cmd('docker save -o '+dockerfilename+' '+dockername)
    if ziptype == 'xz': # 压缩率最高，但是压缩慢。一个实测例子：94M->35M, 压缩约46秒，解压约5秒
        if wexist(dockerfilename) and not wexist(dockerfilename+'.xz'): 
            wzip2xz(dockerfilename, dockerfilename+'.xz')
    if ziptype == 'gz': # 压缩率较低，但是压缩快。一个实测例子：94M->46M, 压缩约5秒，解压约1~2秒
        if wexist(dockerfilename) and not wexist(dockerfilename+'.gz'): 
            wzip2gz(dockerfilename, dockerfilename+'.gz')
    if ziptype == 'xz': dockerfilename = dockerfilename+'.xz'; localfilename = localfilename+'.xz'
    if ziptype == 'gz': dockerfilename = dockerfilename+'.gz'; localfilename = localfilename+'.gz'
    wdownload(localfilename, dockerfilename)
    wls()

def update_a_docker(wksp, imagename, localfilename, dockerfilename, ziptype=None):
    # 将 docker 镜像上传到服务器上并加载
    wrun_cmd, wrun_cmd_loop, wexist, wls, wdownload, wupdate, wremove = make_workspace_run_cmd(wksp)
    wzip2gz, wzip2xz, unzipgz, unzipxz = make_zipper(wksp)
    if not wexist(dockerfilename): wupdate(localfilename, dockerfilename)
    if ziptype == 'gz': 
        if not wexist(dockerfilename.rsplit('.', 1)[0]):
            unzipgz(dockerfilename); 
    if ziptype == 'xz': 
        if not wexist(dockerfilename.rsplit('.', 1)[0]):
            unzipxz(dockerfilename); 
    if ziptype == 'gz': dockerfilename = dockerfilename.rsplit('.', 1)[0]
    if ziptype == 'xz': dockerfilename = dockerfilename.rsplit('.', 1)[0]
    wrun_cmd('docker load -i ' + dockerfilename)
    wrun_cmd('docker images')
    wls()

# 这里的 openresty 版本 openresty-1.25.3.1
# make ja3 openresty skey: 111
# 1dlyice|GYvhPW|lHl^?M<PE5I?y!a>!Ydv*4AR*21Rl{O5Z@}*tUXf39lYBW;}MS_&@bQV{RNAI$yR<LH{l0D6<}&djwJEG2&yKFF>f~97#iX9Nc^xNm-?=Nh_Px<fojp4NisU6qSo5oW*djR`tuu;snqTL}WZYa&m}=l7l)KDKX=yBQij9ps|1Yd**ZJj56{RBe03IHg{bo=v#^V(Fq<p&qSfN?ym5J4^MZ9-eU?%E8^E$Uhz7)*J~2iD+Ep3H|ElyT>pw7qJ!EtChd9QA06lxEDN_s68{mab3v<Ipk~RQikQ(g7F5VBHkpMk<pw`enN1{N+EmkW1~pa9^hSY(1Q0Qqi;`Nx8eHX|H7;LCJLP@A>?8~}XrHN}i^O?t*X8)+4X;W0Z%&2lyV|_DSo&vbryoE2w`0%{Y`>1JEYh*DVg2+j{6D+5J!53HXet@p()QR)+rx9`w0yBU8^B*LJ`7}VB1m~iPa1f?WoIRHLFAdOGRUr|CFA9qh$3#&lVy~6uvEvnI}<$oPWjE*mwC^&b%U}ND?&!rRFFGG`|qys+1Rn}6+p7h3u}Z|I#X<<PnBU-3OI0LX4bjRpM1In6WE@MQ%a34@6)e>eCduT|Aa|+EH*}&BwmZ{<Jj)4f)by<;$GrL4iBTkKAgDHT!m&psbjf_*4^I*9oI&jj%=LWs_8vncp*`dB2vQKFe<W@ogY_h*mVwIM#Y{%p4K~$`WWa@qN5FwPlvWq1rPUz0FC9M4_{m%rO6CI&>$YmEyh{A)2Y6m+9cp5%ZM=($Dd#I1nGBpypXdk&X8<g`o!&mh^{V&rO(Rki>>L_nyR9BRVJG_zI=9tXT@>m<3mymcKjPbj5$RNA|0Hsy&Ia4_fg{J6P;rL+K@-6B~7ACgl#%*sYPNl4^BPc(Y)XRbcdE+!qt8x<RjYnYWBg{FJyz*85GvM{b9lmCRk}%#{mk@R%ZPf@Xu8TAPbs!0k-1WH3yphpSp|0?n~q$vGQ(27Z`8U5BiwR$*Ig({=n{01jezxYTHMwf>_h^%E<dDdbC0<f4+t;gwk9$

def check_is_in_docker(name):
    global print
    _print = print
    print = lambda *a,**kw:None
    r = run_cmd('docker ps -a --filter "name='+name+'"')
    is_in = False
    is_run = False
    for i in r.splitlines():
        if i.strip().endswith(' '+name):
            is_in = True
    r = run_cmd('docker ps --filter "name='+name+'"')
    for i in r.splitlines():
        if i.strip().endswith(' '+name):
            is_run = True
    print = _print
    return is_in, is_run

def check_images(imagename):
    ####################
    return False
    global print
    _print = print
    print = lambda *a,**kw:None
    r = len(run_cmd('docker images ' + imagename).strip().splitlines()) == 2
    print = _print
    return r

def install_gogs(sconfig=None):
    if not sconfig:
        if not load_config():
            return
    make_global_ssh(sconfig)
    wrun_cmd, wrun_cmd_loop, wexist, wls, wdownload, wupdate, wremove = make_workspace_run_cmd(workspace)
    wzip2gz, wzip2xz, unzipgz, unzipxz = make_zipper(workspace)
    # 初始化 gogs ，用于个人代码存储仓库
    imagename = 'gogs/gogs:latest'
    if not check_images(imagename): install(imagename)
    else: print('  [*] image:' +imagename+ ' install')
    is_in, is_run = check_is_in_docker('gogs')
    if not is_in:
        wrun_cmd('docker run --name=gogs -p 10022:22 -p 10880:3000 -v /var/gogs:/data gogs/gogs:latest')
    elif not is_run:
        wrun_cmd('docker start gogs')
    else: pass
    print('run gogs!')

def install_openresty(sconfig=None):
    if not sconfig:
        if not load_config():
            return
    make_global_ssh(sconfig)
    wrun_cmd, wrun_cmd_loop, wexist, wls, wdownload, wupdate, wremove = make_workspace_run_cmd(workspace)
    wzip2gz, wzip2xz, unzipgz, unzipxz = make_zipper(workspace)
    # 初始化 openresty 工具库，用于反向代理或者负载均衡一类
    imagename = 'openresty/openresty:latest'
    if not check_images(imagename): install(imagename)
    else: print('  [*] image:' +imagename+ ' install')

def install_openresty_ja3(sconfig=None):
    if not sconfig:
        if not load_config():
            return
    make_global_ssh(sconfig)
    wrun_cmd, wrun_cmd_loop, wexist, wls, wdownload, wupdate, wremove = make_workspace_run_cmd(workspace)
    wzip2gz, wzip2xz, unzipgz, unzipxz = make_zipper(workspace)
    # 初始化 openresty 工具库，用于反向代理或者负载均衡一类
    imagename = 'cilame/openresty_ja3:latest'
    if not check_images(imagename): install(imagename)
    else: print('  [*] image:' +imagename+ ' install')

def install_nodejs(sconfig=None):
    if not sconfig:
        if not load_config():
            return
    make_global_ssh(sconfig)
    wrun_cmd, wrun_cmd_loop, wexist, wls, wdownload, wupdate, wremove = make_workspace_run_cmd(workspace)
    wzip2gz, wzip2xz, unzipgz, unzipxz = make_zipper(workspace)
    # 初始化 nodejs 工具库，用于快速构建 nodejs 服务
    imagename = 'node:alpine'
    if not check_images(imagename): install(imagename)
    else: print('  [*] image:' +imagename+ ' install')

def get_fpath(modulename):
    try:
        vvv_docker_gogs = __import__(modulename)
        path = os.path.split(vvv_docker_gogs.__file__)[0]
        for i in os.listdir(path):
            if i.endswith('xz'):
                fpath = os.path.join(path, i)
                print('find docker pack. ' + fpath)
                return fpath
    except Exception as e:
        if 'No module' in str(e):
            print('-----------------------------------')
            print(modulename + ' not install, use pip install -- download')
            print('commond:')
            print('    pip install ' + modulename)
        raise e

def install(imagename):
    if imagename == "gogs" or imagename == 'gogs/gogs:latest': 
        fpath = get_fpath('vvv_docker_gogs')
        if not fpath: return
        update_a_docker(workspace, 'gogs/gogs:latest', fpath, 'gogs.tar.xz', ziptype='xz')
    if imagename == "nodejs" or imagename == 'node:alpine': 
        fpath = get_fpath('vvv_docker_nodejs')
        if not fpath: return
        update_a_docker(workspace, 'node:alpine', fpath, 'node21.tar.xz', ziptype='xz')
    if imagename == "python" or imagename == 'cilame/py310:alpine': 
        fpath = get_fpath('vvv_docker_python')
        if not fpath: return
        update_a_docker(workspace, 'cilame/py310:alpine', fpath, 'py310.tar.xz', ziptype='xz')
    if imagename == "openresty" or imagename == 'openresty/openresty:latest': 
        fpath = get_fpath('vvv_docker_openresty')
        if not fpath: return
        update_a_docker(workspace, 'openresty/openresty:latest', fpath, 'openresty.tar.xz', ziptype='xz')
    if imagename == "openresty_ja3" or imagename == 'cilame/openresty_ja3:latest': 
        fpath = get_fpath('vvv_docker_openresty_ja3')
        if not fpath: return
        update_a_docker(workspace, 'cilame/openresty_ja3:latest', fpath, 'openresty_ja3.tar.xz', ziptype='xz')

def load_config(sconfig=None, space=None):
    global workspace
    if space:
        workspace = space
    if not sconfig:
        filepath = os.path.join(os.path.expanduser("~"), 'vvv_dockerrc.json')
        if not os.path.isfile(filepath):
            print('no config file')
            return
        with open(filepath, encoding='utf8') as f:
            jdata = f.read()
        sconfig = json.loads(jdata)
    if not make_global_ssh(sconfig):
        print('no all config')
        return
    return True

def execute():
    filepath = os.path.join(os.path.expanduser("~"), 'vvv_dockerrc.json')
    argv = sys.argv
    tools = ['gogs','openresty','openresty_ja3','nodejs','python']
    print('v_docker :::: [ {} ]'.format(' '.join(argv)))
    if len(argv) == 1:
        print('[*] ================== install: only update in server docker ==================')
        if not os.path.isfile(filepath):
            print('[*] if you first use: pls use v_docker config set your server. !!!')
            print('')
        print('[install]:  v_docker install')
        print('[config]:   v_docker config')
        print('[config]:   v_docker help')
        for t in tools:
            print('[tool]:', t)
        return
    if len(argv) > 1:
        if argv[1] == 'help':
            if len(argv) > 2:
                if argv[2] == 'python':
                    print('\n');print(test_python().strip())
                    return
                elif argv[2] == 'nodejs':
                    print('\n');print(test_nodejs().strip())
                    return
                elif argv[2] == 'openresty':
                    print('\n');print(test_nginx('openresty').strip())
                    return
                elif argv[2] == 'openresty_ja3':
                    print('\n');print(test_nginx('openresty_ja3').strip())
                    return
            print('pls use v_docker help [python/nodejs/openresty/openresty_ja3]')
            print('eg.')
            print('  cmd> v_docker help python')
        if argv[1] == 'config':
            if len(argv) > 2:
                d = {}
                for i in argv[2:]:
                    if '=' in i:
                        k, v = i.split('=', 1)
                        d[k] = v
                jdata = json.dumps(d, indent=4)
                with open(filepath, 'w', encoding='utf8') as f:
                    f.write(jdata)
                print(jdata)
            else:
                if os.path.isfile(filepath):
                    with open(filepath, encoding='utf8') as f:
                        jdata = f.read()
                    print(jdata)
                else:
                    print('no config file', filepath)
        if argv[1] == 'install':
            if not load_config():
                print('load config fail.')
                return 
            if len(argv) > 2:
                if argv[2] in tools:
                    return install(argv[2])
                print('no pack:', argv[2])
            else:
                for t in tools:
                    install(t)

def __setup():
    from setuptools import setup
    setup(
        # pip install twine
        # python setup.py bdist_wheel && twine upload dist/*
        name = "vvv_docker",
        version = "0.0.5",
        packages = ["vvv_docker"],
        entry_points={
            'console_scripts': [
                'v_docker = vvv_docker:execute',
            ]
        },
        install_requires=[
           'paramiko',
        ],
        package_data ={
            "vvv_docker":[
                '*.xz',
            ]
        },
    )







if __name__ == '__main__':
    with open('../config.json', encoding='utf8') as f: sconfig = json.loads(f.read())
    make_global_ssh(sconfig)
    wrun_cmd, wrun_cmd_loop, wexist, wls, wdownload, wupdate, wremove = make_workspace_run_cmd(workspace)
    wzip2gz, wzip2xz, unzipgz, unzipxz = make_zipper(workspace)
    # wremove('gogs.tar')
    # wremove('gogs.tar.xz')
    # wremove('openresty_ja3.tar')
    # wremove('openresty_ja3.tar.xz')
    # wremove('node21.tar')
    # wremove('node21.tar.xz')
    # wls()
    # run_cmd('docker ps')
    # run_cmd('docker images')
    # run_cmd('docker images alpine:latest')
    # exit()
    # run_cmd('docker stop gogs')

    # install_gogs(sconfig)
    # install_openresty_ja3(sconfig)
    # install_nodejs(sconfig)

    download_a_docker('/root/vvv/workspace', 'cilame/py310:alpine', './py310.tar', 'py310.tar', ziptype='xz')
    # download_a_docker('/root/vvv/workspace', 'openresty/openresty:latest', './openresty.tar', 'openresty.tar', ziptype='xz')
    # download_a_docker('/root/vvv/workspace', 'gogs/gogs:latest', './gogs.tar', 'gogs.tar', ziptype='xz')
    # download_a_docker('/root/vvv/workspace', 'cilame/openresty_ja3:latest', './openresty_ja3.tar', 'openresty_ja3.tar', ziptype='xz')
    # download_a_docker('/root/vvv/workspace', 'node:alpine', './node21.tar', 'node21.tar', ziptype='xz')

    # update_a_docker('/root/vvv/workspace', 'gogs/gogs:latest', './gogs.tar.xz', 'gogs.tar.xz', ziptype='xz')
    # update_a_docker('/root/vvv/workspace', 'cilame/openresty_ja3:latest', './openresty_ja3.tar.xz', 'openresty_ja3.tar.xz', ziptype='xz')
    # update_a_docker('/root/vvv/workspace', 'node:alpine', './node21.tar.xz', 'node21.tar.xz', ziptype='xz')


    # 如何使用 gogs/gogs:latest
    # docker run --name=gogs -p 10022:22 -p 10880:3000 -v /var/gogs:/data gogs/gogs:latest
    # docker start gogs

    # 如何使用 cilame/openresty_ja3:latest
    # docker kill vvv_ja3
    # docker rm vvv_ja3
    # docker run --name=vvv_ja3 -p8080:80 -p8443:443 -v ./xxx.key:/usr/local/openresty/nginx/conf/xxx.key -v ./xxx.pem:/usr/local/openresty/nginx/conf/xxx.pem -v ./nginx.conf /usr/local/openresty/nginx/conf/nginx.conf cilame/openresty_ja3:latest
    # docker logs -f vvv_ja3

    # node:alpine
    # 