from setuptools import setup, find_packages

setup(
    name='mschoi-gui',  # 패키지 이름
    version='1.2.1',  # 버전
    author='Ms Choi',  # 작성자
    author_email='mschoi@ybm.co.kr',  # 작성자 이메일
    description='A utility library for database operations, directory management, font settings, GUI operations, and JSON parsing',
    # long_description=open('README.md').read(),  # 긴 설명 (README 파일을 읽어서 사용)
    # long_description_content_type='text/markdown',  # 긴 설명의 형식
    # url='https://github.com/yourusername/mslib',  # 프로젝트 URL
    packages=find_packages(),  # 자동으로 패키지 발견
    classifiers=[  # 패키지의 분류
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 요구되는 최소 Python 버전
    install_requires=[  # 의존성 패키지
        'pandas',
        'sqlalchemy',
        'wxPython',
        'json'
    ],
    package_data={  # 패키지에 포함할 데이터 파일
        '': ['*.md'],  # 예를 들어 README.md 같은 파일 포함
    },
    include_package_data=True,  # 패키지 데이터 포함 여부
    entry_points={  # 콘솔 스크립트 등
        'console_scripts': [
            # 'command_name = module:function',
        ],
    },
)
