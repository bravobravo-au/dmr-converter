# dmrid-converter
Convert the DMR ID Database into a file format for the AnyTone DMR CPS

#installation Binary

1. Download the build dmrconverter-win64-build.zip

2. Unzip the zip file

3. Run dmrconvert.exe

#Installation Python

1. Install the requirements

pip install -r requirements.txt

2. Run dmrconvert

python dmrconvert.py


#command line options

--download=1
Only perform the download from the server

--process=1
Only process the downloaded data

--export=1
Only process and export the data

--filterByCountry=Australia
Only process entries for this country. This relies on the country names and it is an exact match. 


--filterByCallsignPrefix=VK
Only process entries that have callsigns that start with the included prefix.


All configuration is supplied by the settings.py file. This means that you should not need to make changes to code to perform basic tasks. If you use the binary executable distribution you'll need to rebuild the exe to have your settings take effect. If you are using the python method these settings will take place right away. 



