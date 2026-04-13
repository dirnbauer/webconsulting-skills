# Event Dispatch Testing Patterns

## Testing Try/Catch Guarded Event Dispatch

When event dispatch is wrapped in try/catch for robustness, both the success and exception paths need testing.

### Pattern: Guarded Dispatch

```php
// Production code
try {
    $event = $this->eventDispatcher->dispatch(
        new ImageProcessedEvent($filePath, $result)
    );
} catch (\Throwable $e) {
    $this->logger->error('Event listener failed', ['exception' => $e]);
}
```

### Test: Success Path

```php
public function testEventIsDispatched(): void
{
    $eventDispatcher = $this->createMock(EventDispatcherInterface::class);
    $eventDispatcher->expects(self::once())
        ->method('dispatch')
        ->with(self::isInstanceOf(ImageProcessedEvent::class))
        ->willReturnArgument(0); // PSR-14: dispatch() returns the (possibly modified) event

    // ... invoke production code ...
}
```

### Test: Exception Path (Catch Block)

```php
public function testEventDispatchFailureIsLogged(): void
{
    $eventDispatcher = $this->createMock(EventDispatcherInterface::class);
    $eventDispatcher->method('dispatch')
        ->willThrowException(new \RuntimeException('Listener failed'));

    $logger = $this->createMock(LoggerInterface::class);
    $logger->expects(self::once())
        ->method('error')
        ->with(
            self::stringContains('Event listener failed'),
            self::callback(function (array $context): bool {
                return array_key_exists('exception', $context)
                    && $context['exception'] instanceof \Throwable;
            })
        );

    // ... invoke production code, verify it doesn't throw ...
}
```

## Testing PHP Warning/Error Functions

Functions like `getimagesize()` and `file_get_contents()` can trigger PHP warnings when given invalid input.

### Pattern: Suppressed Warning with Return Check

```php
// Production code
$size = @getimagesize($filePath);
if ($size === false) {
    throw new InvalidImageException('Cannot read image dimensions');
}
```

### Test: Warning Trigger Path

```php
public function testInvalidImageThrowsException(): void
{
    $this->expectException(InvalidImageException::class);
    // Pass a non-image file to trigger the getimagesize failure
    $processor->getImageDimensions('/path/to/not-an-image.txt');
}
```

### When to Use @ Suppression

| Context | @ OK? | Reason |
|---------|-------|--------|
| `@mkdir($dir, 0775, true)` | Yes | TOCTOU race condition — dir may be created between check and create |
| `@file_get_contents($path)` | Yes | If return value is checked (`=== false`) |
| `@getimagesize($path)` | Yes | If return value is checked (`=== false`) |
| `@unlink($path)` | Depends | OK in cleanup, not OK if deletion is critical |
