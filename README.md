# Open Source NIST Phantom

Repository to host the open-source NIST phantom. 

## CAD Files for 3D Printing

STL files that can be used for 3d printing are located in the 
[stl-files](https://github.com/kalinared/open-source-nist-phantom/tree/main/stl-files) directory.

Files that can be used for modifying the CAD design of the phantom are located in the 
[stp-files](https://github.com/kalinared/open-source-nist-phantom/tree/main/stp-files) directory.

Fusion 360 files that can be used for modifying the CAD design of the phantom are located in the 
[f3d-files](https://github.com/kalinared/open-source-nist-phantom/tree/main/f3d-files) directory.

## Components
A bill of materials is included in this repository. Specifically, additional components for the phantom can be found at:
* 1x [Oil-Resistant Buna-N O-Ring, 4 mm Wide, 155 mm Inner Diameter](https://www.mcmaster.com/1302N303/)
* 10x [Nylon Plastic Socket Head Screw, M4 x 0.70 mm Thread, 14 mm Long](https://www.mcmaster.com/93640A129/)
* Fill plug, either of:
    * 1x [Plug with External Hex Drive Style, 1/8 NPT](https://www.mcmaster.com/45505K195/)
    * 1x [Plug with External Hex Drive, M10 X1.5 mm Thread Male](https://www.mcmaster.com/4956N25/)

## Tools
* 3.5mm Allen wrench for bolts
* Adjustable wrench for fill plugs
* Bolts:
    * Metric tap: M4 x 0.7
    * (Optional) 3.3mm drill bit
* NPT fill plug:
    * NPT tap (if using NPT fill plug): size: 1/8; threads per inch: 27
    * (Optional) Q drill bit
* Metric fill plug:
    * Metric tap: M10 x 1.5
    * (Optional) 8.5mm drill bit

## Assembly
1. If printing with water permeable material, you may want to coat the inside of the phantom with a waterproof 
layer. [Plasti Dip](https://plastidip.com/our-products/plasti-dip/) can work well for this.
1. The bolt holes and fill port may need to be expanded if the 3D print resulted in a narrower hole. If so, drill out
the holes using the tools described above.
1. Tap the bolt holes and fill port.


## Software
Python code to analyze geometric distortion, snr, and cnr is provided in the [python](https://github.com/kalinared/open-source-nist-phantom/tree/main/python) directory.

---

This repository is developed and maintained
by the Magnetic Imaging group, principally:

- Kathryn Keenan, @katykeenan-nist

Please reach out with questions and comments.
