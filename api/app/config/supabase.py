from supabase import create_client
from app.utils.constants import SUPABASE_SERVICE_KEY
from app.utils.constants import SUPABASE_ANON_KEY
from app.utils.constants import SUPABASE_API_URL

supabase = create_client(SUPABASE_API_URL, SUPABASE_ANON_KEY)
supabase_dev = create_client(SUPABASE_API_URL, SUPABASE_SERVICE_KEY)
