const getPersektor = async () => {
  const response = await fetch("http://localhost:8000/sektor_bruto");
  const data = await response.json();
  return data;
};

const Persektor = async () => {
  const data_persektor = await getPersektor();
  return (
    <div>
      {data_persektor.map((data) => (
        <li key={data.kd_kategori}>{data.nm_kategori}</li>
      ))}
    </div>
  );
};

export default Persektor;
