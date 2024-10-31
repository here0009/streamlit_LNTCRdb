#  Web Service for Lung Cancer TCR db based on Streamlit

Code for http://lungtcr.com/

## Install

You cant install [miniconda](https://docs.anaconda.com/miniconda/miniconda-install/), and using conda to install the required packages to run the script

```bash
conda env create -f env.yml
```

## Run method

If you want to use the mail service, you can rename `send_mail_template.py` to `send_mail.py` and edit it.
You can specify your configuratiomn in the `.streamlit\config.toml` file according to [streamlit](https://docs.streamlit.io/develop/api-reference/configuration/config.toml).

```bash
conda activate streamlit
streamlit run Lung_Cancer_TCR_DB.py > launch.log 2>&1 &
```
