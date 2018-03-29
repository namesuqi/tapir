import flv_parse
import pycurl
import threading
import sys
import time


TIME_INTERVAL = 10
BUFFERINT_TIME = 500

process_data = None
buffer_data = None


def format_time(x, pos=None):
    timeArray = time.localtime(x)
    return time.strftime("%H:%M:%S", timeArray)


def duration_time(x):
    s = x % 60
    x /= 60
    m = x % 60
    x /= 60
    return "%02d:%02d:%02d" % (x, m, s)


class BufferInfo:

    def __init__(self):
        self.timer = threading.Timer(5, self.update)
        pass

    def start(self):
        self.bufferTime = 0
        self.lastTimeStamp = 0
        self.update_cnt = 0
        self.buffering = time.time()
        self.last_real_time = time.time()
        self.startup_time = time.time()
        self.duration = 0
        self.startup = False
        # self.timer.start()

    def addTag(self, pos, timestamp, size):
        self.bufferTime += (timestamp - self.lastTimeStamp)
        self.lastTimeStamp = timestamp
        if self.bufferTime > 2000:
            self.bufferTime -= 500
            self.duration += 0.5
        if self.buffering and self.bufferTime > BUFFERINT_TIME:
            if not self.startup:
                self.startup = True
            self.buffering = 0

    def update(self):
        spend = (time.time() * 1000 - self.last_real_time)
        if self.buffering:
            if self.bufferTime > BUFFERINT_TIME:
                self.bufferTime -= spend
                self.duration += spend / 1000
        else:
            self.bufferTime -= spend
            self.duration += spend / 1000
        self.last_real_time = time.time() * 1000

        if self.bufferTime <= 0:
            self.bufferTime = 0
            if self.buffering == 0:
                self.buffering = time.time()


class ProcessData:

    def __init__(self):
        self.buffer_info = BufferInfo()

    def OpenClientReq(self):
        self.start()

    def CloseClientReq(self):
        self.stop()

    def start(self):
        self.parser = flv_parse.FLVParse()
        self.last_timestamp = 0
        self.frame_time_total = 0
        self.frame_count = 0

    def stop(self):
        self.last_timestamp = 0

    def body_callback(self, buf):
        self.parser.parse(buf, self.tag_callback)

    def timestamp_verify(self, delta):
        if self.frame_count > 0:
            avg = self.frame_time_total / self.frame_count
            diff = avg - delta
            if diff < 0:
                diff = -diff
            if diff > 10:
                pass
        if delta > 0:
            self.frame_time_total += delta
            self.frame_count += 1

    def tag_callback(self, pos, timestamp, vtype, size):
        if vtype == 9:
            delta = timestamp - self.last_timestamp
            self.timestamp_verify(delta)
            self.last_timestamp = timestamp
        if vtype == 18:
            pass


def bytes_coming(buf):
    time.sleep(0.05)
    current = time.localtime()
    time_str = time.strftime("%H%M%S", current)
    print time_str
    process_data.body_callback(buf)


def cur_thread(url):
    print "cur thread...." + url
    global process_data
    cur = pycurl.Curl()
    cur.setopt(cur.URL, url)
    # cur.setopt(cur.SPEED_DOWNLOAD, 2097152)
    cur.setopt(cur.WRITEFUNCTION, bytes_coming)
    process_data.OpenClientReq()
    cur.perform()
    cur.close()
    process_data.CloseClientReq()

if __name__ == '__main__':
    url = "http://127.0.0.1:32717/live_flv/user/simshi?url=http://flv.srs.cloutropy.com/wasu/test.flv"
    pro_data = ProcessData()
    process_data = pro_data
    if len(sys.argv) > 1:
        url = sys.argv[1]

    if url:
        t = threading.Thread(target=cur_thread, args=(url,))
        t.start()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

