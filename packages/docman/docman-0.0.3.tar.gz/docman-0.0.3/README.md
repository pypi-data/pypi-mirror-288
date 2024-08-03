# DocMan - Document Manager

    DocMan is a simple text based document manager.
    It currently has zero dependencies on other packages.

## Be aware

If you think this is a normal file manager you will be disappointed.
It is designed as a recursive document manager based on files and links.
It provides the appearance of a hierarchy while having a shallow directory tree.
This is so that multiple associations can easily be created to the same folder.

A database contains folders and files.
A folder can contain references to other folders.
A folder can contain files.

All folders are stored in the **Database/** directory on the file system as a directory per folder.
All references to folders are created as symbolic links in the directory.
All files in the folder are stored in the directory for the folder.

A database does not support creating references to files.

## Commands

The following commands are supported:

    MENU
    LIST
    LIST LIKE <pattern>...
    LIST LINKS
    LIST LINKS LIKE <pattern>...
    LIST AGAIN
    LIST LINKS AGAIN
    VIEW <index>
    OPEN <index>
    RENAME <index> TO <new-name>
    GO TO <index>
    GOTO <index>
    GO BACK
    RETURN
    DELETE <index>
    HELP <command>
    QUIT
    EXIT

## INSTALLATION

    pip install --user --upgrade docman

## RUNNING

    docman
    or
    docman -f <start-folder>

## ENVIRONMENT VARIABLES

    DOCMAN_HOME = Default <start-folder> for docman

## PROJECT STATUS

    This project is just starting and is alpha status. 
    It is subject to change.
    Please keep this in mind if you intend using it.

## LICENSE

    MIT License
