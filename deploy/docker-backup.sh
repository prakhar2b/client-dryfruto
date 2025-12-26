#!/bin/bash

#===========================================
# DryFruto - Docker Backup Script
#===========================================

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

BACKUP_DIR="/var/backups/dryfruto"
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/var/www/dryfruto"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  DryFruto - Docker Backup${NC}"
echo -e "${GREEN}========================================${NC}"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup MongoDB from Docker
echo -e "${YELLOW}Backing up MongoDB...${NC}"
docker exec dryfruto-mongodb mongodump --db dryfruto --archive=/tmp/mongodb_backup.archive
docker cp dryfruto-mongodb:/tmp/mongodb_backup.archive $BACKUP_DIR/mongodb_$DATE.archive
docker exec dryfruto-mongodb rm /tmp/mongodb_backup.archive

# Backup uploads volume
echo -e "${YELLOW}Backing up uploads...${NC}"
docker run --rm -v dryfruto_uploads_data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/uploads_$DATE.tar.gz -C /data .

# Remove old backups (older than 7 days)
echo -e "${YELLOW}Cleaning old backups...${NC}"
find $BACKUP_DIR -type f -mtime +7 -delete

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Backup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Backups saved to: ${YELLOW}$BACKUP_DIR${NC}"
ls -lh $BACKUP_DIR
