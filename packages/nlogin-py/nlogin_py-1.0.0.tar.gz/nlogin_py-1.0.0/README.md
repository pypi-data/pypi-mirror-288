<div id="nlogin-logo" align="center">
    <br />
    <img src="https://www.nickuc.com/static/assets/img/nlogin.svg" alt="nLogin Logo" width="500"/>
    <h3>Integrate nLogin with your website, forum and/or store.</h3>
</div>

# Installation
On PyPI: <a href="https://pypi.org/project/nlogin_py/" target="_blank">https://pypi.org/project/nlogin_py/</a>

In terminal: `pip install nlogin_py`

## Usage:
1. <a href="#instantiation">Instantiating the nLogin class</a>
2. <a href="#verifying-the-password">Verifying the Password</a>
3. <a href="#registering-a-player">Registering a Player</a>
4. <a href="#changing-the-password">Changing the Password</a>

### <div id="instantiation">Instantiation</div>

```python
from nlogin_py import Nlogin

# Creates an instance
nlogin = Nlogin("localhost", "root", "", "nlogin", False)
```

### <div id="verifying-the-password">Verifying the Password</div>


```python
from nlogin_py import Nlogin

# Creates an instance
nlogin = Nlogin("localhost", "root", "", "nlogin", False)

# Fetches the user identifier (search, mode)
user_id = nlogin.fetch_user_id("Player", Nlogin.FETCH_WITH_LAST_NAME)

# Verifies the password
is_valid = nlogin.verify_password(user_id, "password123")
```


### <div id="registering-a-player">Registering a Player</div>

```python
from nlogin_py import Nlogin

# Creates an instance
nlogin = Nlogin("localhost", "root", "", "nlogin", False)

# Registers a player (username, plain password, e-mail, mojang id (optional), bedrock id (optional))
success = nlogin.register("Player", "password123", "youremail@domain.com")
```

### <div id="changing-the-password">Changing the Password</div>

```python
from nlogin_py import Nlogin

# Creates an instance
nlogin = Nlogin("localhost", "root", "", "nlogin", False)

# Fetches the user identifier (search, mode)
user_id = nlogin.fetch_user_id("Player", Nlogin.FETCH_WITH_LAST_NAME)

# Changes the password (user identifier, new plain password)
success = nlogin.change_password(user_id, "newpassword123")
```

## <div id="license">License</div>

This project is licensed under the GNU General Public License v3.0.

## <div id="reference">Reference</div>

I used a <a href="https://github.com/nickuc-com/nLogin-Web" target="_blank">PHP package</a> from the author of the nLogin plugin. My package is an almost exact copy written in Python.
