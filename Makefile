.PHONY: install test run dashboard server report bench diagrams clean zip all help
help:
	@echo "make install | test | run | dashboard | server | report | bench | diagrams | clean | zip"
install:
	pip install -r requirements.txt
test:
	python3 -m unittest discover -s . -p "test_*.py"
run:
	./radiation.sh all
dashboard:
	streamlit run streamlit_app.py
server:
	python3 server.py
report:
	python3 report.py
bench:
	python3 compare_languages.py
diagrams:
	python3 diagrams.py && python3 diagrams_extra.py
clean:
	rm -rf __pycache__ *.pyc *.egg-info build
zip: clean
	zip -j ../heat-radiation.zip * .gitignore
