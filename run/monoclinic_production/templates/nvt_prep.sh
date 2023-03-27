cp ../../../../relaxation_symmetric/relaxation/geometry.in.next_step geometry.in.primitive
vibes utils make-supercell -n {{ size }}  --deviation 0 -o geometry.in.supercell geometry.in.primitive
vibes utils create-samples geometry.in.supercell -T 10
mv geometry.in.supercell.0010K geometry.in
