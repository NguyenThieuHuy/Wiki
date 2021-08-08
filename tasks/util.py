import re


from django.core.files.base import ContentFile
from django.core.files.storage import default_storage



def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(subject, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{subject}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))
    

def delete_entry(subject):
    filename = f"entries/{subject}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)


    
def get_entry(subject):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{subject}.md")
        return f.read().decode("utf8")
    except FileNotFoundError:
        return None
        