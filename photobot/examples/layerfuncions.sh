#!/bin/sh
python3 Layer_colorize.py
python3 'explore_gradients 1.py'

python3 Layer_filter_boxblur.py
python3 Layer_filter_contour.py
python3 Layer_filter_edge_enhance_more.py
python3 Layer_filter_edge_enhance.py
python3 Layer_filter_emboss.py
python3 Layer_filter_find_edges.py
python3 Layer_function_add_modulo.py
python3 Layer_function_add.py
python3 Layer_function_autocontrast.py
python3 Layer_function_brightness.py
python3 Layer_function_color.py
python3 Layer_function_contrast.py
python3 Layer_function_difference.py
python3 Layer_function_flip.py
python3 Layer_function_hue.py
python3 Layer_function_mask.py
python3 Layer_function_multiply.py
python3 Layer_function_opacity.py
python3 Layer_function_overlay.py
python3 Layer_function_posterize.py
python3 Layer_function_screen.py
python3 Layer_function_select.py
python3 Layer_function_solarize.py
python3 Layer_function_subtract_modulo.py
python3 Layer_function_subtract.py