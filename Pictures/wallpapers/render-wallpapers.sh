#!/usr/bin/env bash
# vim: set ft=sh tabstop=4 expandtab :
min_width=3840
min_height=2160
cd "$(dirname "$0")"
for i in *.svg; do
    width="$(inkscape -W "$i")"
    height="$(inkscape -H "$i")"
    w2h_ratio="$(echo "${width}/${height}" | bc -lq)"
    h2w_ratio="$(echo "${height}/${width}" | bc -lq)"
    height_diff="$(echo "${min_height} - ${height}" | bc -lq)"
    width_diff="$(echo "${min_width} - ${width}" | bc -lq)"
    # If too small in one or both axes
    if [ "$(echo "${width_diff} > 0.0" | bc -lq)" -ne 0 ] || [ "$(echo -n "${height_diff} > 0.0" | bc -lq)" -ne 0 ]; then
        # Width is farther away than height?
        if [ "$(echo "${width_diff} > ${height_diff}" | bc -lq)" -ne 0 ]; then # Width *is* farther away than height
            width="$min_width"
            height="$(echo "${min_width} * ${h2w_ratio}" | bc -lq)"
        else # Height farther away or equal in distance to width
            height="$min_height"
            width="$(echo "${min_height} * ${w2h_ratio}" | bc -lq)"
        fi
    fi
    width="$(ceil "$width")"
    height="$(ceil "$height")"
    inkscape --export-type=png --export-width="${width}" --export-height="${height}" "$i"
done
