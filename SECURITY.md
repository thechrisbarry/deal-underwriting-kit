# Security

## Reporting a problem

Open a GitHub issue. Please do not include real API keys, real owner names, or
any personal information in the report.

## If you build on this

This repo ships **no** credentials and calls only free public endpoints. The
moment you add a paid provider, these apply:

1. **Keys live in `.env` only.** Never in code, never in a report, never
   committed. `.env` is gitignored; `.env.example` shows the shape.
2. **Never ship a key to a browser.** Any key in client-side code is public.
3. **Set a hard spend cap in each provider's own console** before your first
   call. Rate limiting in your code is not the last line of defense.
4. **Run the free checks first** so most candidates fail out before you spend.
5. **If you put a web form on it:** validate input against a schema at the
   boundary, reject unexpected fields, parameterize every database query, and
   rate-limit **by IP** on any public endpoint — user-based limits are useless
   where there is no user.
6. **Enforce every permission server-side**, re-derived from the session. Never
   trust a role or ID sent by the client.
7. **Don't hand-roll auth.** Use an established provider.

## Handling other people's data

This tooling touches public records about **private individuals**, often people
in financial distress.

- **Don't publish owner names, phone numbers or email addresses.** The example
  in this repo is anonymized on purpose.
- Marketing-sourced skip-trace data is **not** credit-bureau data. Never use it
  to screen a tenant or make a credit decision.
- A phone number you bought is **not consent to call it.** Scrub against
  do-not-call lists first, keep a suppression list, honor opt-outs.
- Check each vendor's terms before storing or redistributing their data. Some
  explicitly forbid both.
