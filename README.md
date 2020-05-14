# IPChanger

## Description
IPChanger uses TOR commands to request a new exit node, thus getting you a shiny new external IP address.  It does this via 
the local TOR proxy to get a new ip address via TOR. You will then need to use something like proxychains to leverage this 
new ipaddress. Duh

##Why use this tool?
* You want to map out the TOR network (probably a bad idea)
* You are trying to get around CAPTCHAs (probably a bad idea)
* 1 word: Girls LOVE TOR HACKERS (IDK what that even means, so great idea)
* Because it was acceptable in the 80s (https://www.youtube.com/watch?v=dOV5WXISM24)

## Installation
Installation is easy and free:

IPChanger expects a lot of things to be able to run correctly:
* Requires Linux Operating System
* Requires TOR installed and have a configured ControlPort for controller applications
* Doesnt require ProxyChains to work, but requires ProxyChains to work -- if you know what I mean ;)


# TOR Installation Instructions 
1. Install Linux TOR Client:

    ```sh
    $ sudo apt install tor 
    ```

2. Generate the HashedControlPassword needed to control the Tor proxy:

    ```sh
    $ tor --hash-password ""
    ```

3. Edit the /etc/tor/torrc file and uncomment 'ControlPort', CookieAuthenication, and 'HashedControlPassword'. Replace the example hash with the hash you generated above:

    ```sh
    $ sudo nano /etc/torrc
    ```
   The file should look similar to this (hash will be different)
    ```sh
    ## The port on which Tor will listen for local connections from Tor
    ## controller applications, as documented in control-spec.txt.
    ControlPort 9051
    ## If you enable the controlport, be sure to enable one of these
    ## authentication methods, to prevent attackers from accessing it.
    HashedControlPassword 16:238FDE9CC88B6265608CEB18405196EFDB15F7FD1100D0663B0498D223
    CookieAuthentication 1
    ```

4. Restart the Tor client:

    ```sh
    $ sudo service tor restart
    ```

