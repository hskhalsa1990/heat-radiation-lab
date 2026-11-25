#!/usr/bin/env bash
# Usage: ./radiation.sh            -> CSV "T,flux" table (awk)
#        ./radiation.sh bench N    -> checksum over N evaluations
#        ./radiation.sh all        -> full Python pipeline
case "$1" in
  bench) awk -v n="$2" 'BEGIN{s=5.670374419e-8; sum=0; for(i=0;i<n;i++){t=300+(i%900); t2=t*t; s2=300*300; sum+=0.8*s*(t2*t2-s2*s2)}; printf "checksum,%.6e\n", sum}' ;;
  all)
    python3 make_data.py && python3 data_clean.py && python3 analyst.py &&
    python3 visualize.py && python3 diagrams.py && python3 diagrams_extra.py &&
    python3 -m unittest discover -s . -p "test_*.py" && python3 hybrid_ml.py &&
    python3 ml_model.py && python3 dl_model.py && python3 cv_thermal.py &&
    python3 report.py && python3 compare_languages.py
    if command -v Rscript >/dev/null; then Rscript analysis.R; fi ;;
  *) awk 'BEGIN{s=5.670374419e-8; for(t=400;t<=1200;t+=200){t2=t*t; s2=300*300; printf "%d,%.3f\n", t, 0.8*s*(t2*t2-s2*s2)}}' ;;
esac
