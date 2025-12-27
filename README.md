# DryFruto - Premium Dry Fruits E-Commerce

A full-stack e-commerce application for selling premium dry fruits, nuts, and seeds.

## Tech Stack

- **Frontend:** React + TailwindCSS + Shadcn UI
- **Backend:** FastAPI (Python)
- **Database:** MongoDB 6.0
- **Server:** Nginx (Reverse Proxy)
- **Containerization:** Docker + Docker Compose

## Deploy on Hostinger VPS with Docker Manager

### Prerequisites
- Hostinger VPS with Docker Manager enabled
- GitHub repository with this code
- Domain name pointed to your VPS IP (optional but recommended)

### Deployment Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```
   Make sure all Docker files are in your repository root:
   - `docker-compose.yml`
   - `Dockerfile.backend`
   - `Dockerfile.nginx`
   - `nginx.conf`

2. **In Hostinger VPS Panel:**
   - Go to **Docker** → **Docker Compose**
   - Click **Create New**
   - Select **From GitHub URL**
   - Enter your repository URL: `https://github.com/YOUR_USERNAME/YOUR_REPO`
   - Select branch: `main`
   - Click **Deploy**

3. **Wait for deployment**
   - Hostinger will pull the code and run `docker-compose up -d --build`
   - First deployment may take 5-10 minutes (downloading images, building)

4. **Access your site**
   - Your site will be available at your VPS IP: `http://YOUR_VPS_IP`
   - Or your domain: `http://your-domain.com`
   - Admin panel: `http://your-domain/admin`

## Docker Services

| Service | Description | Port |
|---------|-------------|------|
| nginx | Frontend + Reverse Proxy | 80 |
| backend | FastAPI API Server | 8001 (internal) |
| mongodb | Database | 27017 (internal) |

## Environment Variables

The following are configured automatically in docker-compose.yml:

- `MONGO_URL` - MongoDB connection string
- `DB_NAME` - Database name (dryfruto)

## Useful Docker Commands

SSH into your VPS and run:

```bash
# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose up -d --build

# Stop all services
docker-compose down
```

## Updating Your Site

1. Push changes to GitHub
2. SSH into your VPS
3. Navigate to your project directory
4. Run:
   ```bash
   git pull origin main
   docker-compose up -d --build
   ```

## Data Persistence

The following data is persisted in Docker volumes:
- `mongodb_data` - Database files
- `uploads_data` - User uploaded images

## Admin Panel

Access the admin panel at `/admin` to:
- Manage products and categories
- Update hero slides and testimonials
- Configure site settings
- View form submissions
- Update About Us page content

## Support

For issues or questions, please create an issue in the GitHub repository.
