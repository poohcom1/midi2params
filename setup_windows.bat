:: set up a virtual environment
py -m virtualenv -p %LOCALAPPDATA%\Programs\Python\Python37\python.exe midi2params_env || echo Error: Virtualenv not found! && exit /b
cd midi2params_env
call .\Scripts\activate

:: install some python packages
py -m pip install -r requirements.txt
pip install ipykernel
git clone https://github.com/poohcom1/midi2params.git
cd midi2params
py -m pip install -e .
:: install the kernel into jupyter, so that it can be used
:: in the notebook
py -m ipykernel install --user --name=midi2params_env

:: get necessary data
@REM ./get_data.sh
@REM ./get_checkpoint.sh
@REM ./get_model.sh
