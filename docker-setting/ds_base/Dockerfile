FROM registry.gitlab.com/nyker510/analysis-template/cpu

USER root

COPY local-requirements.txt requirements.txt

RUN pip install -U pip && \
  pip install -U -r requirements.txt

# install nodejs
RUN curl -sL https://deb.nodesource.com/setup_12.x |bash - \
    && apt-get install -y --no-install-recommends \
    nodejs

# install kite

## RUN cd && \
##     wget https://linux.kite.com/dls/linux/current && \
##     chmod 777 current && \
##     sed -i 's/"--no-launch"//g' current > /dev/null && \
##     ./current --install ./kite-installer && \
##     pip3 install --no-cache-dir "jupyterlab-kite>=2.0.2"

# install jupyterlab_variableinspector
RUN pip3 install --upgrade --no-cache-dir \
    black \
    isort \
    jupyterlab_code_formatter \
    && jupyter labextension install \
        @ryantam626/jupyterlab_code_formatter \
    && jupyter serverextension enable --py jupyterlab_code_formatter

# install jupyterlab_variableinspector
RUN pip3 install --no-cache-dir lckr-jupyterlab-variableinspector

# # install GPU Dashboards
# RUN pip3 install --no-cache-dir jupyterlab-nvdashboard \
#     && jupyter labextension install \
#         jupyterlab-nvdashboard
# 
# # install Tensorboard
# RUN pip3 install --no-cache-dir tensorflow-gpu \
#     tensorboard \
#     jupyter-tensorboard \
#     && jupyter labextension install \
#         jupyterlab_tensorboard \
#     && jupyter serverextension enable --py jupyterlab_tensorboard
# 


USER penguin

CMD [ "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--NotebookApp.token="]