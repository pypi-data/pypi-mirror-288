# DNS Utils


## Why this library ?
I worked on DNS/Registrar analysis and consolidation over a few months, and something we quickly notice is that:
- Not everything is standardized (E.g. Whois database response)
- The RFC are very verbose and most developers don't want to go through all of it for their simple needs.
- The way the DNS respond is not ideal for development. For example, it is better to receive an empty list when no records are found that throwing an error "No record".
- Having typing on these information helps a lot and ensure correctness.


This library is, for a big part, a layer on top of dnspython

## Current status.
This library was developed progressively over months as per needed.
It was not designed upfront as many things got discovered along the road.
- The current API is supposed to be stable, the underlying behaviour might be changed for correctness if needed, but retrocompatibility should be kept.
- The current API will hopefully be completed with additional features.

## Contributing

Contributions are more than welcomed, but respect the process:
- **Always open an issue first**: PR without issue won't be accepted and might even be closed immediatly.
  The issue is here to discuss the needs and proposals and serves as an history. Try to be as explicit as possible and provide links/screenshots when possible.
  NOTE: You can open an issue even if you are not the one that will implement the feature/bug fix.
- You can start opening a PR once the issue got approved. Please, immediatly reference the issue on your PR so that people knows the issue is being handled.

Don't forget that this module is not meant for your own personal usage, but for everyone's.
For features not implementing strictly the RFC, we might split it in an optional feature of the module.
