# Event Scheduler Demo

A simple demonstration of event-driven scheduling and processing in Python using asyncio. This project showcases how to build a basic event system with job scheduling capabilities.

## 🎯 What This Demo Shows

- **Event-Driven Architecture**: How to implement a simple event system with producers and consumers
- **Asynchronous Processing**: Using Python's asyncio for non-blocking event handling
- **Job Scheduling**: Basic integration with APScheduler for timed tasks
- **Graceful Shutdown**: Proper signal handling and cleanup
- **Event Correlation**: Tracking related events with correlation IDs

## 📋 Prerequisites

- Python 3.13 or higher
- Basic understanding of async/await in Python

## 🛠️ Quick Start

1. **Clone and install**:

   ```bash
   git clone <repository-url>
   cd event-scheduler
   uv install
   ```

2. **Run the demo**:

   ```bash
   python main.py
   ```

3. **Watch the logs** to see events being processed:
   ```
   2024-01-01 12:00:00.000 | INFO | Starting the scheduler application...
   2024-01-01 12:00:00.001 | INFO | Event handler started
   2024-01-01 12:00:00.002 | INFO | ✅ Application is running. Press Ctrl+C to stop.
   ```

## 🏗️ How It Works

The demo consists of a few key components:

```
main.py                  # Entry point
├── EventScheduler       # Orchestrates everything
├── JobManager           # Handles scheduled jobs
├── EventHandler         # Manages event queue
└── Event System         # Defines event types and data
```

### Core Concepts

1. **Events**: Simple data structures that represent something that happened
2. **Event Queue**: An async queue that holds events waiting to be processed
3. **Event Handler**: Processes events from the queue asynchronously
4. **Job Manager**: Schedules and manages recurring tasks

## 📝 Event Types

The demo supports these basic event types:

- `JOB_STARTED`: When a scheduled job begins
- `JOB_COMPLETED`: When a job finishes successfully
- `JOB_FAILED`: When a job encounters an error
- `SHUTDOWN_REQUESTED`: When the app should stop

## 🔧 Configuration

Create a `.env` file to customize behavior:

```env
APP_ENV=local
LOG_LEVEL=INFO
```

| Setting     | Default | Description                                        |
| ----------- | ------- | -------------------------------------------------- |
| `APP_ENV`   | `local` | Application environment (local/staging/production) |
| `LOG_LEVEL` | `INFO`  | Logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL)  |

## 🚀 Extending the Demo

### Adding a Custom Event

1. **Define the event type** in `app/events/event_type.py`:

   ```python
   class EventType(Enum):
       CUSTOM_EVENT = "custom_event"
   ```

2. **Emit the event** in your code:

   ```python
   event = Event.create(
       EventType.CUSTOM_EVENT,
       data={'message': 'Hello World'},
       correlation_id='demo-123'
   )
   await event_handler.emit(event)
   ```

3. **Handle the event** in `job_manager.py`:
   ```python
   async def handle_event(self, event: Event) -> bool:
       if event.type == EventType.CUSTOM_EVENT:
           print(f"Received: {event.data['message']}")
       return True
   ```

### Adding a Scheduled Job

```python
# In job_manager.py
def add_demo_job(self):
    self.add_job(
        func=self.demo_function,
        trigger='interval',
        seconds=10,
        id='demo_job'
    )

async def demo_function(self):
    event = Event.create(
        EventType.JOB_STARTED,
        data={'job_id': 'demo_job', 'timestamp': datetime.now()}
    )
    await self.emit_event(event)
```

## 📚 Learning Points

This demo illustrates several important concepts:

- **Event-Driven Programming**: How to decouple components using events
- **Async/Await Patterns**: Non-blocking I/O and concurrent processing
- **Queue Management**: Handling backpressure and overflow
- **Signal Handling**: Graceful application shutdown
- **Correlation Tracking**: Following related events through a system

## 🤝 Contributing

This is a learning project! Feel free to:

- Add new event types
- Implement different job scheduling patterns
- Add error handling examples
- Create more complex event flows

## 🐛 Troubleshooting

**Common issues:**

- **Import errors**: Make sure you're using Python 3.13+
- **No events showing**: Check that the event handler is running
- **Queue full**: Events are being dropped - check your processing logic

**Getting help:**

1. Check the logs for error messages
2. Verify your Python version
3. Ensure all dependencies are installed
