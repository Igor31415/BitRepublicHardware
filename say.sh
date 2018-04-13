#!/bin/bash
urlencode() {
	python -c 'import urllib, sys; print urllib.quote(sys.argv[1], sys.argv[2])' \
	"$1" "$urlencode_safe"
 }


say() { 
	echo $*
	dest=~;
	data=$*;
	encoded=$(urlencode "$data");
	curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" \
	-o $dest/output.mp3 \
	"http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=${encoded}&tl=fr";
	omxplayer $dest/output.mp3; 
}
say $* 
