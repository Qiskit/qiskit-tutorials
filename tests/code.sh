notebooks=$(find . -name "*.ipynb" -not -path "*/.*" -not -path "./_build/**")

for notebook in ${notebooks}
do
  python -m nbqa black ${notebook} --check || exit 1
  python -m nbqa pylint ${notebook} --fail-under=10 || exit 1
done
