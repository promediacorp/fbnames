ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ printf "%s", $1}' | redis-cli -x -h 172.30.0.242 lpush plist