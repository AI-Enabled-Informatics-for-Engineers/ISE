How to run demos

//Option A In Colab, run:

!git clone https://github.com/AI-Enabled-Informatics-for-Engineers/ISE/new/main/notebooks/week03
%cd https://github.com/AI-Enabled-Informatics-for-Engineers/ISE/new/main/notebooks/week03
!pip -q install pandas numpy matplotlib pandera scipy scikit-learn
!python lecture03_demos.py --out_dir artifacts --show_plots 0
//It will produce artifacts/ with CSVs + PNGs.//

//Option B Azure VM or Local

pip install pandas numpy matplotlib pandera scipy scikit-learn
python lecture03_demos.py --out_dir artifacts --show_plots 0
