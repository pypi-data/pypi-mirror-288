from setuptools import setup, find_packages

setup(
    name="chart-server",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["fastapi==0.111.1", "lightweight-charts==2.0.1"],
    author="Won JeongHoo",
    author_email="clomia.sig@gmail.com",  # 작성자 이메일
    description="lightweight-chart custom python server",  # 패키지 설명
    long_description=open("README.md").read(),  # 패키지 상세 설명
    long_description_content_type="text/markdown",  # 상세 설명 형식
    url="https://github.com/vegaxholdings/chart-server",  # 패키지 URL
    classifiers=[
        "Programming Language :: Python :: 3",  # 사용 언어
        "License :: OSI Approved :: MIT License",  # 라이선스
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # 요구되는 Python 버전
)
