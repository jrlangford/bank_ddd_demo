# Online Bank DDD Demo
A django demo project that loosely implements Domain Driven Design.

Bank Domain: Enabling clients to perform monetary transactions online.

For this demo bounded contexts exactly match subdomains.

Subdomains/Bounded Contexts:
- Identity and Access
- Client Management
- Account Management
- Transactions (Core)

## Quickstart
```
pipenv install
pipenv shell
./manage.py migrate
./manage.py runserver
```

## Architecture
Implementing an architecture with full layer isolation in Django is not practical.
This demo implements an architecture in which layers are partially isolated.

Layers:
- Interface
- Application
- Domain
- Infrastructure

## DDD Mapping

### Directory structure

```
root/
    README.md
    manage.py
    ...
    project/
        settings.py
        drivers/
            asgi.py
            wsgi.py
        interface/
            urls.py
            views.py
            serializers.py
            tests.py
            ...
        application/
            services.py
            tests.py
            ...
        domain/
            moduleA/
                models.py
                services.py
                tests.py
                ...
            moduleB/
            moduleC/
            ...
    external-moduleA/
    external-moduleB/
    ...
```

If required, the interface and application directories can have one additional level of nested directories.

### Patterns

**Entities** -> Django models  
**Value Objects** -> Python frozen dataclasses  
**Aggregates** -> Django models with foreign keys to other Django models in the same module  
**Repositories** -> Django Managers  
**Factories** -> Custom factory classes  

In order to honor this mappings and reduce coupling, the following restrictions must be imposed

- Only create entities through their respective factories.
    - All factories should accept only value objects
    - Validate value objects upon creation
- Perform all repository creations and updates in a single atomic step whenever possible.
    - Do not defer entity id creation to the DB
    - Use UUID-4 for entity ids

## Tradeoffs
It is desirable to structure the project in a way that removes django dependencies from the application and domain layers; however, this implies losing some out-of-the-box django functionality.

Django features we choose to keep:
- Automatic Admin interface for Django Models
    - Consistency between entities and the models seen in the Admin
- Pre-defined flexible repository functions
- Automatic model serialization/deserialization

DDD and layer architecture features we lose:
- Full model expression with tactical DDD patterns
- Decoupling of the application and domain layers from django libraries
