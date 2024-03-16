.PHONY: tests_movies
tests_movies:
	docker build -t movies_tests --target tests ./movies_api
	docker run --rm --name t_cont --network=auth_sprint_2_default movies_tests
