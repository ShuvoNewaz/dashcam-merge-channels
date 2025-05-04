date="$1"
front="/media/shuvo/8258-1113/video/F"
back="/media/shuvo/8258-1113/video/R"
left="/media/shuvo/8258-1113/video/FL"
right="/media/shuvo/8258-1113/video/FR"
front_dest="Front/"
back_dest="Back/"
right_dest="Right/"
left_dest="Left/"

mkdir -p "$front_dest" "$back_dest" "$right_dest" "$left_dest"

declare -A dir_map
dir_map["$front"]="$front_dest"
dir_map["$back"]="$back_dest"
dir_map["$left"]="$left_dest"
dir_map["$right"]="$right_dest"

for src_dir in "${!dir_map[@]}"; do
    dest_dir="${dir_map[$src_dir]}"
    find "$src_dir" -type f -name "*$date*.ts" -exec cp "{}"  "$dest_dir" \;
done