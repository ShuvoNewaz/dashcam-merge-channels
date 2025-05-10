date="$1"
dashCamHome="$2"

front_dest="Front/"
back_dest="Back/"
right_dest="Right/"
left_dest="Left/"

mkdir -p "$front_dest" "$back_dest" "$right_dest" "$left_dest"

for src_folder in "video" "park" "event";
do
    front="${dashCamHome}/${src_folder}/F"
    back="${dashCamHome}/${src_folder}/R"
    left="${dashCamHome}/${src_folder}/FL"
    right="${dashCamHome}/${src_folder}/FR"

    declare -A dir_map
    dir_map["$front"]="$front_dest"
    dir_map["$back"]="$back_dest"
    dir_map["$left"]="$left_dest"
    dir_map["$right"]="$right_dest"

    for src_dir in "${!dir_map[@]}";
    do
        dest_dir="${dir_map[$src_dir]}"
        find "$src_dir" -type f -name "*$date*.ts" -exec cp "{}"  "$dest_dir" \;
    done
    unset dir_map
done