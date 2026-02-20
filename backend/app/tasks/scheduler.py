"""
Background task scheduler using APScheduler.
Runs weekly analysis and stores summary in the database every Monday at 00:00.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def run_weekly_analysis():
    """
    Scheduled task: analyze last 7 days of decisions per user,
    compute category breakdown, and store in weekly_summary table.
    """
    try:
        from datetime import datetime, timedelta
        from app.db import SessionLocal
        from app.models.decision import Decision
        from app.models.weekly_summary import WeeklySummary
        from app.services.weekly_analyzer import analyze_weekly_activity
        import uuid

        db = SessionLocal()
        try:
            week_ago = datetime.utcnow() - timedelta(days=7)

            # Get distinct user_ids
            user_ids = [r[0] for r in db.query(Decision.user_id).distinct().all()]

            for user_id in user_ids:
                recent = (
                    db.query(Decision)
                    .filter(Decision.user_id == user_id, Decision.created_at >= week_ago)
                    .all()
                )
                decision_dicts = [
                    {"category_tag": d.category_tag} for d in recent
                ]
                summary_pcts = analyze_weekly_activity(decision_dicts)

                entry = WeeklySummary(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    week_start=datetime.utcnow().date(),
                    **summary_pcts,
                )
                db.add(entry)
            db.commit()
            logger.info("Weekly analysis completed for %d users", len(user_ids))
        finally:
            db.close()
    except Exception as e:
        logger.error("Weekly analysis failed: %s", e)


def start_scheduler():
    scheduler.add_job(
        run_weekly_analysis,
        trigger=CronTrigger(day_of_week="mon", hour=0, minute=0),
        id="weekly_analysis",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started")


def stop_scheduler():
    scheduler.shutdown()
