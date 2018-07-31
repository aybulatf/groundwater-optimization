FROM python:3.6-jessie

RUN apt-get update \
    && apt-get install -y g++ gfortran wget unzip make

RUN pip install numpy \
    && pip install scipy \
    && pip install flopy \
    && pip install pika

# installing pymake
RUN pip install https://github.com/modflowpy/pymake/zipball/master

#installing mf2005
RUN wget https://water.usgs.gov/ogw/modflow/MODFLOW-2005_v1.12.00/MF2005.1_12u.zip \
    && unzip MF2005.1_12u.zip \
    && rm MF2005.1_12u.zip \
    && python -m pymake.pymake ./MF2005.1_12u/src /usr/local/bin/mf2005

#installing mfnwt
RUN wget https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT_1.1.4.zip \
    && unzip MODFLOW-NWT_1.1.4.zip \
    && rm MODFLOW-NWT_1.1.4.zip \
    && python -m pymake.pymake ./MODFLOW-NWT_1.1.4/src /usr/local/bin/mfnwt

#installing mt3dusgs
RUN wget https://water.usgs.gov/ogw/mt3d-usgs/mt3d-usgs_1.0.zip \
    && unzip mt3d-usgs_1.0.zip \
    && rm mt3d-usgs_1.0.zip \
    && python -m pymake.pymake ./mt3d-usgs_Distribution/src /usr/local/bin/mt3dusgs