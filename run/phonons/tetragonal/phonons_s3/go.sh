ln -s ../relaxation/relaxation/geometry.in.next_step geometry.in
vibes run phonopy
vibes out phonopy --full phonopy/trajectory.son