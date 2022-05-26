Some python tests scripts for communicating with the Bitmain BM1387 
bitcoin mining ASIC.

The BM1387 is most famously used in the Antminer S9. AS far as I know 
there is no datasheet available for the BM1387, so this is all reverse engineering.

- The Gekkoscience Newpac is a USB stick miner that has 2 BM1387 chips. 
  The [wareck modified cgminer](https://github.com/wareck/cgminer-gekko/blob/master/driver-gekko.c) that supports the newpac has some hints about how to
  communicate with the BM1387.
  

- [Braiins](https://braiins.com) has released an open source OS for the Antminer S9 
  that also has [some hints](https://github.com/braiins/braiins/blob/bos-devel/open/bosminer/bosminer-am1-s9/src/bm1387.rs) on communicating with chains of BM1387s via the Antminer's FPGA