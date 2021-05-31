FROM python:3.6

RUN apt-get update

RUN mkdir -p /usr/src/vim-manager

COPY rl_git/rl/plugins/VIM/openstack/vim-manager /usr/src/vim-manager

WORKDIR /usr/src/vim-manager

RUN pip install .

EXPOSE 8001

CMD ["vim-manager --config-file config.conf.exemple run"]