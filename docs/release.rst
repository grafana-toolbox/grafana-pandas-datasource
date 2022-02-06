#################################
Grafana pandas datasource release
#################################


1. Update changelog in ``CHANGES.rst``
2. Tag repository with ``git tag <new release>``
3. Update repository with ``git push && git push --tags``
4. Build packages with ``pip install build && python -m build``
5. Upload packages with ``pip install twine && twine upload dist/*``
