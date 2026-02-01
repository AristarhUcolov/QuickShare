"""
Translations for QuickShare - LAN File Transfer
Переводы для QuickShare - Передача Файлов по Локальной Сети
"""

TRANSLATIONS = {
    'en': {
        # Header
        'title': '🚀 QuickShare',
        'files_count': 'Files',
        'total_size': 'Total Size',
        'qr_button': '📱 QR Code',
        
        # Upload
        'upload_title': 'Upload Files',
        'upload_desc': 'Click or drag files/folders here',
        'select_files': '📁 Select Files',
        'select_folder': '📂 Select Folder',
        
        # Search & Sort
        'search_placeholder': 'Search files...',
        'sort_name': '📝 Name',
        'sort_size': '💾 Size',
        'sort_date': '📅 Date',
        
        # File actions
        'download_zip': '⬇️ ZIP',
        'download': '⬇️',
        'delete': '🗑️',
        
        # Empty state
        'no_files': 'No files yet',
        'no_files_desc': 'Upload your first file to start!',
        
        # Progress
        'uploading': 'Uploading...',
        
        # QR Modal
        'scan_qr': '📱 Scan QR Code',
        'close': 'Close',
        
        # Confirmations
        'confirm_delete': 'Delete',
        
        # Size units
        'size_b': 'B',
        'size_kb': 'KB',
        'size_mb': 'MB',
        'size_gb': 'GB',
        'size_tb': 'TB',
        
        # Language
        'language': 'Language',
        'lang_switch': 'RU'
    },
    'ru': {
        # Header
        'title': '🚀 QuickShare',
        'files_count': 'Файлов',
        'total_size': 'Общий размер',
        'qr_button': '📱 QR-код',
        
        # Upload
        'upload_title': 'Загрузить файлы',
        'upload_desc': 'Нажмите или перетащите файлы/папки сюда',
        'select_files': '📁 Выбрать файлы',
        'select_folder': '📂 Выбрать папку',
        
        # Search & Sort
        'search_placeholder': 'Поиск файлов...',
        'sort_name': '📝 Имя',
        'sort_size': '💾 Размер',
        'sort_date': '📅 Дата',
        
        # File actions
        'download_zip': '⬇️ ZIP',
        'download': '⬇️',
        'delete': '🗑️',
        
        # Empty state
        'no_files': 'Файлов пока нет',
        'no_files_desc': 'Загрузите первый файл чтобы начать!',
        
        # Progress
        'uploading': 'Загрузка...',
        
        # QR Modal
        'scan_qr': '📱 Сканируйте QR-код',
        'close': 'Закрыть',
        
        # Confirmations
        'confirm_delete': 'Удалить',
        
        # Size units
        'size_b': 'Б',
        'size_kb': 'КБ',
        'size_mb': 'МБ',
        'size_gb': 'ГБ',
        'size_tb': 'ТБ',
        
        # Language
        'language': 'Язык',
        'lang_switch': 'EN'
    }
}

def get_translation(lang='en'):
    """Get translation dictionary for language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en'])
