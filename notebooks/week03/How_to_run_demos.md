How to run demos

//Option A In Colab, run:

//line 1:
!git clone https://github.com/AI-Enabled-Informatics-for-Engineers/ISE.git
line 2:
%cd ISE/notebooks/week03
//line 3:
!pip -q install pandas numpy matplotlib scikit-learn
//line 4:
!python lecture03_demos.py --out_dir artifacts --show_plots 1

//It will produce artifacts/ with CSVs + PNGs.//

//Option B Azure VM or Local

pip install pandas numpy matplotlib pandera scipy scikit-learn
python lecture03_demos.py --out_dir artifacts --show_plots 0
