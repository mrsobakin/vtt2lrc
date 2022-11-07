import sys
from datetime import datetime, timedelta, timezone


def parse_time(time_str):
    dt = datetime.strptime(time_str.strip(), "%H:%M:%S.%f")
    return dt


def format_time(time):
    return time.strftime("%M:%S.%f")[:8]


DEFAULT_THRESHOLD = timedelta(seconds=2)


def vtt2lrc(vtt, header=True, threshold=DEFAULT_THRESHOLD):
    lrc = ""
    
    if header:
        lrc += "[re:vtt2lrc]\n"

    last_end = parse_time("23:59:59.99") # Insanely big value

    for chunk in vtt.split("\n\n")[1:]:
        if not chunk:
            continue
        
        time, text = chunk.split("\n", 1)
        begin, end = map(parse_time, time.split("-->"))
        
        if begin - last_end > threshold:
            lrc += f"[{format_time(last_end)}]\n"
            
        lrc += f"[{format_time(begin)}] {text}\n"
        
        last_end = end
        
    lrc += f"[{format_time(last_end)}]\n"
    
    return lrc


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        vtt = f.read()
    
    print(vtt2lrc(vtt))
