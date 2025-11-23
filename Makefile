CONTAINER = boto3-py-demo
IMAGE = boto3-py
SRC ?= $(CURDIR)

.PHONY: build clean

build: clean
	docker --debug build -t $(IMAGE) .
	docker run -dit --name $(CONTAINER) \
		--env-file .env \
		--mount type=bind,source=$(SRC)/src,destination=/work \
		$(IMAGE)

clean:
	-docker container stop $(CONTAINER)
	-docker container rm $(CONTAINER)
	-docker image rm $(IMAGE)
