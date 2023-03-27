vibes utils make-supercell -dd 9 9 9 600_geometry.in.primitive
vibes utils make-supercell -dd 8 8 8 600_geometry.in.primitive
vibes utils make-supercell -dd 7 7 7 600_geometry.in.primitive
vibes utils make-supercell -dd 6 6 6 600_geometry.in.primitive
vibes utils make-supercell -dd 5 5 5 600_geometry.in.primitive
vibes utils make-supercell -dd 4 4 4 600_geometry.in.primitive
vibes utils make-supercell -dd 3 3 3 600_geometry.in.primitive
vibes utils make-supercell -dd 2 2 2 600_geometry.in.primitive

vibes utils create-samples 600_geometry.in.primitive.supercell_96 -T 10
vibes utils create-samples 600_geometry.in.primitive.supercell_324 -T 10
vibes utils create-samples 600_geometry.in.primitive.supercell_768 -T 10
vibes utils create-samples 600_geometry.in.primitive.supercell_1500 -T 10
vibes utils create-samples 600_geometry.in.primitive.supercell_2592 -T 10
vibes utils create-samples 600_geometry.in.primitive.supercell_4116 -T 10
vibes utils create-samples 600_geometry.in.primitive.supercell_6144 -T 10
vibes utils create-samples 600_geometry.in.primitive.supercell_8748 -T 10

