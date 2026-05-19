# 9. CLI Commands (TYPO3 v14)

Continues `typo3-update` from [full guide](full-guide.md).

## 9. CLI Commands (TYPO3 v14)

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Command;

use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;
use TYPO3\CMS\Core\Core\Bootstrap;

#[AsCommand(
    name: 'myext:process',
    description: 'Process items in the extension',
)]
final class ProcessCommand extends Command
{
    protected function configure(): void
    {
        $this
            ->addArgument('type', InputArgument::REQUIRED, 'The type to process')
            ->addOption('force', 'f', InputOption::VALUE_NONE, 'Force processing');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);
        
        // Initialize backend for DataHandler operations
        Bootstrap::initializeBackendAuthentication();
        
        $type = $input->getArgument('type');
        $force = $input->getOption('force');
        
        $io->title('Processing: ' . $type);
        
        // Your logic here...
        
        $io->success('Processing completed successfully');
        
        return Command::SUCCESS;
    }
}
```

### Command Registration

With **`autoconfigure: true`** in `Services.yaml` defaults, **`#[AsCommand]` is enough** — you do **not** need the `console.command` tag unless autoconfigure is disabled for that service.

```yaml
# Optional — only when not using #[AsCommand] + autoconfigure
services:
  Vendor\Extension\Command\ProcessCommand:
    tags:
      - name: console.command
```
