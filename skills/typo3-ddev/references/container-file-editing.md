# Writing files / running PHP inside the container

Author the file with your editor and `docker cp` it in, then run a simple
command. Don't fight shell quoting with nested heredocs or `php -r` —
apostrophes and `$` get mangled through `ddev exec`, and the container path may
not be host-mounted, so the project mount isn't always reachable from where you
wrote the file.

```bash
# {sitename} = name: from .ddev/config.yaml; {VERSION} = the TYPO3 version vhost.
# The web container is ddev-{sitename}-web. Note: $DDEV_SITENAME is only set
# INSIDE the container, so on the host shell name it explicitly.
docker cp snippet.php ddev-{sitename}-web:/tmp/snippet.php
ddev exec 'cat /tmp/snippet.php >> /var/www/html/v{VERSION}/config/system/additional.php'  # append config
ddev exec 'php /tmp/snippet.php'                                                            # run a probe
```
