while read line; do sudo kill -9 $line; done < process_id
rm -f process_id