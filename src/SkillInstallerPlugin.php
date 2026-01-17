<?php

declare(strict_types=1);

namespace WebConsulting\AgentSkills;

use Composer\Composer;
use Composer\EventDispatcher\EventSubscriberInterface;
use Composer\IO\IOInterface;
use Composer\Plugin\PluginInterface;
use Composer\Script\Event;
use Composer\Script\ScriptEvents;

/**
 * Composer plugin that installs Claude Agent Skills after package installation.
 *
 * This plugin runs the install.sh script to deploy skills to ~/.claude/skills
 * and generate Cursor rules from SKILL.md files.
 */
final class SkillInstallerPlugin implements PluginInterface, EventSubscriberInterface
{
    private Composer $composer;
    private IOInterface $io;

    public function activate(Composer $composer, IOInterface $io): void
    {
        $this->composer = $composer;
        $this->io = $io;
    }

    public function deactivate(Composer $composer, IOInterface $io): void
    {
        // Nothing to do on deactivation
    }

    public function uninstall(Composer $composer, IOInterface $io): void
    {
        // Nothing to do on uninstall
    }

    public static function getSubscribedEvents(): array
    {
        return [
            ScriptEvents::POST_INSTALL_CMD => 'onPostInstall',
            ScriptEvents::POST_UPDATE_CMD => 'onPostUpdate',
        ];
    }

    public function onPostInstall(Event $event): void
    {
        $this->runInstaller();
    }

    public function onPostUpdate(Event $event): void
    {
        $this->runInstaller();
    }

    private function runInstaller(): void
    {
        $vendorDir = $this->composer->getConfig()->get('vendor-dir');
        $packageDir = $vendorDir . '/webconsulting/webconsulting-skills';
        $installScript = $packageDir . '/install.sh';

        if (!file_exists($installScript)) {
            $this->io->writeError('<warning>install.sh not found in package directory</warning>');
            return;
        }

        $this->io->write('<info>Installing Claude Agent Skills...</info>');

        $exitCode = 0;
        passthru('bash ' . escapeshellarg($installScript), $exitCode);

        if ($exitCode === 0) {
            $this->io->write('<info>Claude Agent Skills installed successfully.</info>');
        } else {
            $this->io->writeError('<error>Failed to install Claude Agent Skills (exit code: ' . $exitCode . ')</error>');
        }
    }
}
