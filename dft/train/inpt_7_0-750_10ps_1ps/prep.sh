cp ../relaxation/relaxation/geometry.in.next_step geometry.in.primitive
vibes utils make-supercell geometry.in.primitive -n 96
mv geometry.in.primitive.supercell_96 geometry.in.supercell
vibes utils create-samples geometry.in.supercell -T 10
mv geometry.in.supercell.0010K geometry.in