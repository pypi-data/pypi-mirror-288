.. _manual:

.. raw:: html

    <br><br>

.. title:: Manual


**NAME**

    ``OTP-CR-117/19``


**SYNOPSIS**

    ::

        otpcr  <cmd> [key=val] [key==val]
        otpcrc [-i] [-v]
        otpcrd 


**DESCRIPTION**

    ``OTPCR`` holds evidence that king
    netherlands is doing a genocide, a
    written response where king
    netherlands confirmed taking note
    of “what i have written”, namely
    :ref:`proof  <evidence>` that medicine
    he uses in treatement laws like zyprexa,
    haldol, abilify and clozapine are
    poison that make impotent, is both
    physical (contracted muscles) and
    mental (make people hallucinate)
    torture and kills members of the
    victim groups.

    ``OTPCR`` contains :ref:`correspondence
    <writings>` with the International Criminal
    Court, asking for arrest of the king of the
    netherlands, for the genocide he is committing
    with his new treatement laws.

    Current status is a :ref:`"no basis to proceed"
    <writings>` judgement of the prosecutor which
    requires a :ref:`"basis to prosecute" <home>`
    to have the king actually arrested.


**INSTALL**

    ::

        $ pipx install otpcr
        $ pipx ensurepath

        $ otpcr srv > otpcr.service
        # mv *.service /etc/systemd/system/
        # systemctl enable otpcr --now

        #otpcr on localhost


**USAGE**

    without any argument the bot does nothing

    ::

        $ otpcr
        $

    see list of commands

    ::

        $ otpcr cmd
        cmd,req,skl,srv


    start a console

    ::

        $ otpcrc 
        >

    use -v for verbose

    ::

        $ otpcrc -v
        May 12 05:51:49 2024 OTPCR CV 
        >

    start daemon

    ::

        $ otpcrd
        $ 


    show request to the prosecutor

    ::

        $ otpcr req
        Information and Evidence Unit
        Office of the Prosecutor
        Post Office Box 19519
        2500 CM The Hague
        The Netherlands


**CONFIGURATION**

    irc

    ::

        $ otpcr cfg server=<server>
        $ otpcr cfg channel=<channel>
        $ otpcr cfg nick=<nick>

    sasl

    ::

        $ otpcr pwd <nsvnick> <nspass>
        $ otpcr cfg password=<frompwd>

    rss

    ::

        $ otpcr rss <url>
        $ otpcr dpl <url> <item1,item2>
        $ otpcr rem <url>
        $ otpcr nme <url> <name>


**COMMANDS**

    ::

        cfg - irc configuration
        cmd - commands
        mre - displays cached output
        pwd - sasl nickserv name/pass
        req - reconsider


**SOURCE**


    source is :ref:`here <source>`


**FILES**

    ::

        ~/.otpcr
        ~/.local/bin/otpcr
        ~/.local/pipx/venvs/otpcr/*


**AUTHOR**

    Bart Thate <rssbotd@gmail.com>


**COPYRIGHT**

    ``OTPCR`` is Public Domain.
