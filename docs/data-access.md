# Data Access

> Steps for macOS

## Account

1. You must create an account for data access:
   [create account](https://wiki.earthdata.nasa.gov/display/EL/How+To+Register+For+an+EarthData+Login+Profile)
2. Link account to GES DISC: [link account](https://disc.gsfc.nasa.gov/earthdata-login)

## Setup

Create a `.netrc` file in your home directory.

 ```sh
touch ~/.netrc
 ```

Populate `.netrc` file with credentials (where <uid> is your user name and <password> is your Earthdata Login password without the brackets):

 ```sh
echo 'machine urs.earthdata.nasa.gov login <uid> password <password>' >> ~/.netrc 
 ```

Create a cookie file. This file will be used to persist sessions across calls to wget.

 ```sh
touch ~/.urs_cookies
 ```

> Note: you may need to re-create `.urs_cookies` in case you have already executed `curl` or `wget` without valid authentication.

Change permissions to `.netrc` and `.urs_cookies` files (so only you can access it):

 ```sh
chmod 0600 ~/.netrc ~/.urs_cookies
 ```

Test:

`curl`

```bash
curl -n -c ~/.urs_cookies -b ~/.urs_cookies -LJO --url \
https://tropess.gesdisc.eosdis.nasa.gov/data/TROPESS_Special/TRPSDL2O3CRSWCF.1/doc/TROPESS_West_Coast_Fires_README_2-23-21.pdf
```

`wget`

```bash
wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies \
     --auth-no-challenge=on --keep-session-cookies --content-disposition \
     https://tropess.gesdisc.eosdis.nasa.gov/data/TROPESS_Special/TRPSDL2O3CRSWCF.1/doc/TROPESS_West_Coast_Fires_README_2-23-21.pdf
```

## OpenDAP

> OpenDAP allows you to access TROPESS data directly over Internet without downloading files locally.

Create a `.daprc` file in your home directory that points to your `.urs_cookies` file:

```
echo "HTTP.COOKIEJAR=$HOME/.urs_cookies" > ~/.daprc 
```

## Additional Information

[Overview of GES DISC Data Access](https://disc.gsfc.nasa.gov/data-access)

