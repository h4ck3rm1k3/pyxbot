
cat $1 | sed -e's;</delete>;;g' | sed -e's;<delete>;;g' | sed -e's;osmChange;osm;g' 
