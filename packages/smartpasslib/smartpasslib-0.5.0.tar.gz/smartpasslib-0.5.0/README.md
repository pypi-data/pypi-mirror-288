# Smart Passwords Library <sup>v0.5.0</sup>

***

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/smartlegionlab/smartpasslib)](https://github.com/smartlegionlab/smartpasslib/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/smartpasslib?label=pypi%20downloads)](https://pypi.org/project/smartpasslib/)
![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smartpasslib)
[![PyPI](https://img.shields.io/pypi/v/smartpasslib)](https://pypi.org/project/smartpasslib)
[![GitHub](https://img.shields.io/github/license/smartlegionlab/smartpasslib)](https://github.com/smartlegionlab/smartpasslib/blob/master/LICENSE)
[![PyPI - Format](https://img.shields.io/pypi/format/smartpasslib)](https://pypi.org/project/smartpasslib)

***

## Short Description:
___smartpasslib___ - Cross-platform library for generating smart passwords.

***

Author and developer: ___A.A. Suvorov.___

***

## Supported:

- Linux: All.
- Windows: 7/8/10.
- Termux (Android).

***

## What is news:

smartpasslib 0.5.0 - new improved version of the library.

> WARNING! This version is not backward compatible with previous versions.

- Completely rewritten and improved code.
- Simplified import.
- Fixed errors.
- Added new password generator.

***

## Help:

`pip install smartpasslib`

```python
from smartpasslib import SmartPasswordMaster
login = 'login'
secret = 'secret'
length = 15

smart_password_master = SmartPasswordMaster()

smart_password = smart_password_master.generate_smart_password(login=login, secret=secret, length=length)
smart_password2 = smart_password_master.generate_smart_password(login=login, secret=secret, length=length)
check_passwords = smart_password == smart_password2  # True

key = smart_password_master.generate_public_key(login, secret)

check_data = smart_password_master.check_public_key(login, secret, key)

```

***

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

***

    Licensed under the terms of the BSD 3-Clause License
    (see LICENSE for details).
    Copyright © 2018-2024, A.A. Suvorov
    All rights reserved.