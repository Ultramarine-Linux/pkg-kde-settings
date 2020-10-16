#!/bin/sh

# Restart DBus as shutdown may not be clean leaving failed activation requests that prevent the next login
(sleep 8 && systemctl --user restart dbus.service) &
