# FastAPI + Piccolo

Tried out Piccolo, since it lets you do the schema and models in one step, and simplifies a lot of the CRUD operations. The migrations and admin are also kind of nice, haven't tried the tests yet. Let's talk soon and see what you think. 

Didn't get Poetry working yet...

```bash
pip install -r requirements.txt
```

Run with:

```bash
python main.py
```

and head to the /docs.

I used Postgres since it allows for automatic migrations. Create a Postcres database named `dhrift`. Then run the migrations:

```bash
piccolo migrations forwards dhrift
```

If you want to try the Piccolo admin (kind of like the DJango admin), also run these migrations:

```bash
piccolo migrations forwards session_auth
piccolo migrations forwards user
```

and create an administrative user:

```bash
piccolo user create
```
